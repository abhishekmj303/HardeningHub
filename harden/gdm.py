import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["gdm"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['remove']:
        script += f"sudo apt purge gdm3\n"
        return script
    
    if file_systems_config['disable_user_list']:
        script+= f"""
l_gdmprofile="gdm"
if [ ! -f "/etc/dconf/profile/$l_gdmprofile" ]; then
    echo "Creating profile \"$l_gdmprofile\""
    echo -e "user-db:user\nsystem-db:$l_gdmprofile\nfile-db:/usr/share/$l_gdmprofile/greeter-dconf-defaults" > "/etc/dconf/profile/$l_gdmprofile"
fi
if [ ! -d "/etc/dconf/db/$l_gdmprofile.d/" ]; then
    echo "Creating dconf database directory \"/etc/dconf/db/$l_gdmprofile.d/\""
    mkdir "/etc/dconf/db/$l_gdmprofile.d/"
fi
if ! grep -Piq '^\h*disable-user-list\h*=\h*true\b' "/etc/dconf/db/$l_gdmprofile.d/"*; then
    echo "Creating gdm keyfile for machine-wide settings"
    if ! grep -Piq '^\h*\[org\/gnome\/login-screen\]' "/etc/dconf/db/$l_gdmprofile.d/"*; then
        echo -e "\n[org/gnome/login-screen]\n# Do not show the user list\ndisable-user-list=true" >> "/etc/dconf/db/$l_gdmprofile.d/00-login-screen"
    else
        sed -ri '/^\s*\[org\/gnome\/login-screen\]/ a\# Do not show the user list\ndisable-user-list=true' $(grep -Pil '^\h*\[org\/gnome\/login-screen\]' "/etc/dconf/db/$l_gdmprofile.d/"*)
    fi
fi
dconf update
"""
    if file_systems_config['lock_on_idle']:
        t = file_systems_config['lock_on_idle']
        script += f"""
echo -e "[org/gnome/desktop/session]\nidle-delay=uint32 {t}" | dconf write /org/gnome/desktop/session/idle-delay
echo -e "[org/gnome/desktop/screensaver]\nlock-delay=uint32 1" | dconf write /org/gnome/desktop/screensaver/lock-delay"""
    if file_systems_config['no_override_lockscreen']:
        script += """
l_pkgoutput=""
if command -v dpkg-query > /dev/null 2>&1; then
    l_pq="dpkg-query -W"
elif command -v rpm > /dev/null 2>&1; then
    l_pq="rpm -q"
fi
l_pcl="gdm gdm3"
for l_pn in $l_pcl; do
    $l_pq "$l_pn" > /dev/null 2>&1 && l_pkgoutput="y" && echo -e "\n - Package: \"$l_pn\" exists on the system\n - Remediating configuration if needed"
done
if [ -n "$l_pkgoutput" ]; then
    l_kfd="/etc/dconf/db/$(grep -Psril '^\h*idle-delay\h*=\h*uint32\h+\d+\b' /etc/dconf/db/*/ | awk -F'/' '{split($(NF-1),a,".");print a[1]}').d"  # Set the directory of the key file to be locked
    l_kfd2="/etc/dconf/db/$(grep -Psril '^\h*lock-delay\h*=\h*uint32\h+\d+\b' /etc/dconf/db/*/ | awk -F'/' '{split($(NF-1),a,".");print a[1]}').d"  # Set the directory of the key file to be locked

    if [ -d "$l_kfd" ]; then
        if grep -Prilq '^\h*\/org\/gnome\/desktop\/session\/idle-delay\b' "$l_kfd"; then
            echo " - \"idle-delay\" is locked in \"$(grep -Pril'^\h*\/org\/gnome\/desktop\/session\/idle-delay\b' "$l_kfd")\""
        else
            echo "Creating entry to lock \"idle-delay\""
            [ ! -d "$l_kfd"/locks ] && echo "Creating directory $l_kfd/locks" && mkdir "$l_kfd"/locks
            {
                echo -e '\n# Lock desktop screensaver idle-delay setting'
                echo '/org/gnome/desktop/session/idle-delay'
            } >> "$l_kfd"/locks/00-screensaver
        fi
    else
        echo -e " - \"idle-delay\" is not set so it cannot be locked\n - Please follow Recommendation \"Ensure GDM screen locks when the user is idle\" and follow this Recommendation again"
    fi

    if [ -d "$l_kfd2" ]; then
        if grep -Prilq '^\h*\/org\/gnome\/desktop\/screensaver\/lock-delay\b' "$l_kfd2"; then
            echo " - \"lock-delay\" is locked in \"$(grep -Pril'^\h*\/org\/gnome\/desktop\/screensaver\/lock-delay\b' "$l_kfd2")\""
        else
            echo "Creating entry to lock \"lock-delay\""
            [ ! -d "$l_kfd2"/locks ] && echo "Creating directory $l_kfd2/locks" && mkdir "$l_kfd2"/locks
            {
                echo -e '\n# Lock desktop screensaver lock-delay setting'
                echo '/org/gnome/desktop/screensaver/lock-delay'
            } >> "$l_kfd2"/locks/00-screensaver
        fi
    else
        echo -e " - \"lock-delay\" is not set so it cannot be locked\n - Please follow Recommendation \"Ensure GDM screen locks when the user is idle\" and follow this Recommendation again"
    fi
else
    echo -e " - GNOME Desktop Manager package is not installed on the system\n - Recommendation is not applicable"
fi
"""
    if file_systems_config['disable_automount']:
        script += """
l_pcl="gdm gdm3"  # Space-separated list of packages to check
for l_pn in $l_pcl; do
    $l_pq "$l_pn" > /dev/null 2>&1 && l_pkgoutput="$l_pkgoutput\n - Package: \"$l_pn\" exists on the system\n - Checking configuration"
done
echo -e "$l_pkgoutput"

# Check configuration (If applicable)
if [ -n "$l_pkgoutput" ]; then
    echo -e "$l_pkgoutput"
    
    # Look for existing settings and set variables if they exist
    l_kfile="$(grep -Prils -- '^\h*automount\b' /etc/dconf/db/*.d)"
    l_kfile2="$(grep -Prils -- '^\h*automount-open\b' /etc/dconf/db/*.d)"

    # Set the profile name based on the dconf db directory ({PROFILE_NAME}.d)
    if [ -f "$l_kfile" ]; then
        l_gpname="$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile")"
        echo " - Updating dconf profile name to \"$l_gpname\""
    elif [ -f "$l_kfile2" ]; then
        l_gpname="$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile2")"
        echo " - Updating dconf profile name to \"$l_gpname\""
    fi

    # Check for consistency (Clean up configuration if needed)
    if [ -f "$l_kfile" ] && [ "$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile")" != "$l_gpname" ]; then
        sed -ri "/^\s*automount\s*=/s/^/# /" "$l_kfile"
        l_kfile="/etc/dconf/db/$l_gpname.d/00-media-automount"
    fi

    if [ -f "$l_kfile2" ] && [ "$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile2")" != "$l_gpname" ]; then
        sed -ri "/^\s*automount-open\s*=/s/^/# /" "$l_kfile2"
    fi

    [ -n "$l_kfile" ] && l_kfile="/etc/dconf/db/$l_gpname.d/00-media-automount"

    # Check if the profile file exists
    if grep -Pq "^\h*system-db:$l_gpname\b" /etc/dconf/profile/*; then
        echo -e "\n - Dconf database profile exists in: \"$(grep -Pl "^\h*system-db:$l_gpname\b" /etc/dconf/profile/*)\""
    else
        [ ! -f "/etc/dconf/profile/user" ] && l_gpfile="/etc/dconf/profile/user" || l_gpfile="/etc/dconf/profile/user2"
        echo -e " - Creating dconf database profile"
        {
            echo -e "\nuser-db:user"
            echo "system-db:$l_gpname"
        } >> "$l_gpfile"
    fi

    # Create dconf directory if it doesn't exist
    l_gpdir="/etc/dconf/db/$l_gpname.d"
    if [ -d "$l_gpdir" ]; then
        echo " - The dconf database directory \"$l_gpdir\" exists"
    else
        echo " - Creating dconf database directory \"$l_gpdir\""
        mkdir "$l_gpdir"
    fi

    # Check automount-open setting
    if grep -Pqs '^\h*automount-open\h*=\h*false\b' "$l_kfile"; then
        echo " - \"automount-open\" is set to false in: \"$l_kfile\""
    else
        echo " - Creating \"automount-open\" entry in \"$l_kfile\""
        ! grep -Psq '\^\h*\[org\/gnome\/desktop\/media-handling\]\b' "$l_kfile" && echo '[org/gnome/desktop/media-handling]' >> "$l_kfile"
        sed -ri '/^\s*\[org\/gnome\/desktop\/media-handling\]/a\nautomount-open=false' "$l_kfile"
    fi

    # Check automount setting
    if grep -Pqs '^\h*automount\h*=\h*false\b' "$l_kfile"; then
        echo " - \"automount\" is set to false in: \"$l_kfile\""
    else
        echo " - Creating \"automount\" entry in \"$l_kfile\""
        ! grep -Psq '\^\h*\[org\/gnome\/desktop\/media-handling\]\b' "$l_kfile" && echo '[org/gnome/desktop/media-handling]' >> "$l_kfile"
        sed -ri '/^\s*\[org\/gnome\/desktop\/media-handling\]/a\nautomount=false' "$l_kfile"
    fi
else
    echo -e "\n - GNOME Desktop Manager package is not installed on the system\n - Recommendation is not applicable"
fi
"""

    if file_systems_config['lock_automount']:
        script += """

# Check if GNOME Desktop Manager is installed. If package isn't
installed, recommendation is Not Applicable\n
# determine system's package manager
l_pkgoutput=""
if command -v dpkg-query > /dev/null 2>&1; then
l_pq="dpkg-query -W"
elif command -v rpm > /dev/null 2>&1; then
l_pq="rpm -q"
fi
# Check if GDM is installed
l_pcl="gdm gdm3" # Space seporated list of packages to check
for l_pn in $l_pcl; do
$l_pq "$l_pn" > /dev/null 2>&1 && l_pkgoutput="$l_pkgoutput\n -
Package: \"$l_pn\" exists on the system\n - checking configuration"
done
# Check configuration (If applicable)
if [ -n "$l_pkgoutput" ]; then
l_output="" l_output2=""
# Look for idle-delay to determine profile in use, needed for remaining
tests
l_kfd="/etc/dconf/db/$(grep -Psril '^\h*automount\b' /etc/dconf/db/*/ |
awk -F'/' '{split($(NF-1),a,".");print a[1]}').d" #set directory of key file
to be locked
l_kfd2="/etc/dconf/db/$(grep -Psril '^\h*automount-open\b'
/etc/dconf/db/*/ | awk -F'/' '{split($(NF-1),a,".");print a[1]}').d" #set
directory of key file to be locked
if [ -d "$l_kfd" ]; then # If key file directory doesn't exist, options
can't be locked
if grep -Piq '^\h*\/org/gnome\/desktop\/media-handling\/automount\b'
"$l_kfd"; then
l_output="$l_output\n - \"automount\" is locked in \"$(grep -Pil
'^\h*\/org/gnome\/desktop\/media-handling\/automount\b' "$l_kfd")\""
else
l_output2="$l_output2\n - \"automount\" is not locked"
fi
else
l_output2="$l_output2\n - \"automount\" is not set so it can not be
locked"
fi
if [ -d "$l_kfd2" ]; then # If key file directory doesn't exist,
options can't be locked
if grep -Piq '^\h*\/org/gnome\/desktop\/media-handling\/automount-
open\b' "$l_kfd2"; then
l_output="$l_output\n - \"lautomount-open\" is locked in \"$(grep
-Pril '^\h*\/org/gnome\/desktop\/media-handling\/automount-open\b'
"$l_kfd2")\""
else
l_output2="$l_output2\n - \"automount-open\" is not locked"
fi
else
l_output2="$l_output2\n - \"automount-open\" is not set so it can
not be locked"
fi
else
Page 180
l_output="$l_output\n - GNOME Desktop Manager package is not installed
on the system\n - Recommendation is not applicable"
fi
# Report results. If no failures output in l_output2, we pass
[ -n "$l_pkgoutput" ] && echo -e "\n$l_pkgoutput"
if [ -z "$l_output2" ]; then
echo -e "\n- Audit Result:\n ** PASS **\n$l_output\n"
else
echo -e "\n- Audit Result:\n ** FAIL **\n - Reason(s) for audit
failure:\n$l_output2\n"
[ -n "$l_output" ] && echo -e "\n- Correctly set:\n$l_output\n"
fi
"""
        
    if file_systems_config['disable_autorun']:
        script += """
l_pkgoutput=""
l_output=""
l_output2=""
l_gpname="local"  # Set to the desired dconf profile name (default is local)

# Check if GNOME Desktop Manager is installed. If the package isn't installed, the recommendation is Not Applicable
# Determine the system's package manager
if command -v dpkg-query > /dev/null 2>&1; then
    l_pq="dpkg-query -W"
elif command -v rpm > /dev/null 2>&1; then
    l_pq="rpm -q"
fi

# Check if GDM is installed
l_pcl="gdm gdm3"  # Space-separated list of packages to check
for l_pn in $l_pcl; do
    $l_pq "$l_pn" > /dev/null 2>&1 && l_pkgoutput="$l_pkgoutput\n - Package: \"$l_pn\" exists on the system\n - Checking configuration"
done
echo -e "$l_pkgoutput"

# Check configuration (If applicable)
if [ -n "$l_pkgoutput" ]; then
    echo -e "$l_pkgoutput"
    
    # Look for existing settings and set variables if they exist
    l_kfile="$(grep -Prils -- '^\h*autorun-never\b' /etc/dconf/db/*.d)"
    
    # Set the profile name based on the dconf db directory ({PROFILE_NAME}.d)
    if [ -f "$l_kfile" ]; then
        l_gpname="$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile")"
        echo " - Updating dconf profile name to \"$l_gpname\""
    fi
    [ ! -f "$l_kfile" ] && l_kfile="/etc/dconf/db/$l_gpname.d/00-media-autorun"
    
    # Check if the profile file exists
    if grep -Pq "^\h*system-db:$l_gpname\b" /etc/dconf/profile/*; then
        echo -e "\n - Dconf database profile exists in: \"$(grep -Pl "^\h*system-db:$l_gpname\b" /etc/dconf/profile/*)\""
    else
        [ ! -f "/etc/dconf/profile/user" ] && l_gpfile="/etc/dconf/profile/user" || l_gpfile="/etc/dconf/profile/user2"
        echo -e " - Creating dconf database profile"
        {
            echo -e "\nuser-db:user"
            echo "system-db:$l_gpname"
        } >> "$l_gpfile"
    fi
    
    # Create dconf directory if it doesn't exist
    l_gpdir="/etc/dconf/db/$l_gpname.d"
    if [ -d "$l_gpdir" ]; then
        echo " - The dconf database directory \"$l_gpdir\" exists"
    else
        echo " - Creating dconf database directory \"$l_gpdir\""
        mkdir "$l_gpdir"
    fi
    
    # Check autorun-never setting
    if grep -Pqs '^\h*autorun-never\h*=\h*true\b' "$l_kfile"; then
        echo " - \"autorun-never\" is set to true in: \"$l_kfile\""
    else
        echo " - Creating or updating \"autorun-never\" entry in \"$l_kfile\""
        if grep -Psq '^\h*autorun-never' "$l_kfile"; then
            sed -ri 's/(^\s*autorun-never\s*=\s*)(\S+)(\s*.*)$/\1true \3/' "$l_kfile"
        else
            ! grep -Psq '\^\h*\[org/gnome/desktop/media-handling\]\b' "$l_kfile" && echo '[org/gnome/desktop/media-handling]' >> "$l_kfile"
            sed -ri '/^\s*\[org/gnome/desktop/media-handling\]/a\nautorun-never=true' "$l_kfile"
        fi
    fi
else
    echo -e "\n - GNOME Desktop Manager package is not installed on the system\n - Recommendation is not applicable"
fi

# Update dconf database
dconf update

# Additional script for `no_override_autorun`
if file_systems_config['no_override_autorun']:
    # Check if GNOME Desktop Manager is installed. If the package isn't installed, the recommendation is Not Applicable
    l_pkgoutput=""
    if command -v dpkg-query > /dev/null 2>&1; then
        l_pq="dpkg-query -W"
    elif command -v rpm > /dev/null 2>&1; then
        l_pq="rpm -q"
    fi

    # Check if GDM is installed
    l_pcl="gdm gdm3"  # Space-separated list of packages to check
    for l_pn in $l_pcl; do
        $l_pq "$l_pn" > /dev/null 2>&1 && l_pkgoutput="y" && echo -e "\n - Package: \"$l_pn\" exists on the system\n - Remediating configuration if needed"
    done

    # Check configuration (If applicable)
    if [ -n "$l_pkgoutput" ]; then
        # Look for autorun to determine the profile in use, needed for remaining tests
        l_kfd="/etc/dconf/db/$(grep -Psril '^\h*autorun-never\b' /etc/dconf/db/*/ | awk -F'/' '{split($(NF-1),a,".");print a[1]}').d"  # Set the directory of the key file to be locked

        if [ -d "$l_kfd" ]; then  # If the key file directory doesn't exist, options can't be locked
            if grep -Priq '^\h*\/org/gnome/desktop/media-handling/autorun-never\b' "$l_kfd"; then
                echo " - \"autorun-never\" is locked in \"$(grep -Pril '^\h*\/org/gnome/desktop/media-handling/autorun-never\b' "$l_kfd")\""
            else
                echo " - Creating entry to lock \"autorun-never\""
                [ ! -d "$l_kfd/locks" ] && echo "Creating directory $l_kfd/locks" && mkdir "$l_kfd/locks"
                {
                    echo -e '\n# Lock desktop media-handling autorun-never setting'
                    echo '/org/gnome/desktop/media-handling/autorun-never'
                } >> "$l_kfd/locks/00-media-autorun"
            fi
        else
            echo -e " - \"autorun-never\" is not set, so it cannot be locked\n - Please follow Recommendation \"Ensure GDM autorun-never is enabled\" and follow this Recommendation again"
        fi
    fi
    # Update dconf database
    dconf update
else
    echo -e " - GNOME Desktop Manager package is not installed on the system\n - Recommendation is not applicable"
fi
"""

    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))
