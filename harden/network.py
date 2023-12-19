from harden import config_file

def get_script(config):
    network_config = config["network"]
    # Start with an empty script and build it up
    script = ""

    if network_config['disable_wireless']:
        script += '''
if command -v nmcli >/dev/null 2>&1 ; then
nmcli radio all off
else
if [ -n "$(find /sys/class/net/*/ -type d -name wireless)" ]; then
mname=$(for driverdir in $(find /sys/class/net/*/ -type d -name wireless
| xargs -0 dirname); do basename "$(readlink -f
"$driverdir"/device/driver/module)";done | sort -u)
for dm in $mname; do
echo "install $dm /bin/true" >> /etc/modprobe.d/disable_wireless.conf
done
fi
fi
'''

    if network_config['disable_packet_redirects']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['disable_ip_forwarding']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.ip_forward=0 net.ipv6.conf.all.forwarding=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
IPV6F_CHK()
{
l_ipv6s=""
grubfile=$(find /boot -type f \( -name 'grubenv' -o -name 'grub.conf' -
o -name 'grub.cfg' \) -exec grep -Pl -- '^\h*(kernelopts=|linux|kernel)' {}
\;)
if [ -s "$grubfile" ]; then
! grep -P -- "^\h*(kernelopts=|linux|kernel)" "$grubfile" | grep -vq
-- ipv6.disable=1 && l_ipv6s="disabled"
fi
if grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc && \
grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc
&& \
sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" && \
sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$"; then
l_ipv6s="disabled"
fi
if [ -n "$l_ipv6s" ]; then
echo -e "\n - IPv6 is disabled on the system, \"$l_kpname\" is not
applicable"
else
KPF
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
if grep -q '^net.ipv6.' <<< "$l_kpe"; then
l_kpfile="/etc/sysctl.d/60-netipv6_sysctl.conf"
IPV6F_CHK
else
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF
fi
done
}
'''

    if network_config['reject_source_routed_packets']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0
net.ipv6.conf.all.accept_source_route=0
net.ipv6.conf.default.accept_source_route=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
IPV6F_CHK()
{
l_ipv6s=""
grubfile=$(find /boot -type f \( -name 'grubenv' -o -name 'grub.conf' -
o -name 'grub.cfg' \) -exec grep -Pl -- '^\h*(kernelopts=|linux|kernel)' {}
\;)
if [ -s "$grubfile" ]; then
! grep -P -- "^\h*(kernelopts=|linux|kernel)" "$grubfile" | grep -vq
-- ipv6.disable=1 && l_ipv6s="disabled"
fi
if grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc && \
grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc
&& \
sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" && \
sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$"; then
l_ipv6s="disabled"
fi
if [ -n "$l_ipv6s" ]; then
echo -e "\n - IPv6 is disabled on the system, \"$l_kpname\" is not
applicable"
else
KPF
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
if grep -q '^net.ipv6.' <<< "$l_kpe"; then
l_kpfile="/etc/sysctl.d/60-netipv6_sysctl.conf"
IPV6F_CHK
else
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF
fi
done
}
'''

    if network_config['reject_icmp_redirects']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0 net.ipv6.conf.all.accept_redirects=0
net.ipv6.conf.default.accept_redirects=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
IPV6F_CHK()
{
l_ipv6s=""
grubfile=$(find /boot -type f \( -name 'grubenv' -o -name 'grub.conf' -
o -name 'grub.cfg' \) -exec grep -Pl -- '^\h*(kernelopts=|linux|kernel)' {}
\;)
if [ -s "$grubfile" ]; then
! grep -P -- "^\h*(kernelopts=|linux|kernel)" "$grubfile" | grep -vq
-- ipv6.disable=1 && l_ipv6s="disabled"
fi
if grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc && \
grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc
&& \
sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" && \
sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$"; then
l_ipv6s="disabled"
fi
if [ -n "$l_ipv6s" ]; then
echo -e "\n - IPv6 is disabled on the system, \"$l_kpname\" is not
applicable"
else
KPF
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
if grep -q '^net.ipv6.' <<< "$l_kpe"; then
l_kpfile="/etc/sysctl.d/60-netipv6_sysctl.conf"
IPV6F_CHK
else
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF
fi
done
}
'''

    if network_config['reject_secure_icmp_redirects']:
        script += '''
kernel_parameter_fix()
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.default.secure_redirects=0
net.ipv4.conf.all.secure_redirects=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['log_suspicious_packets']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.all.log_martians=1
net.ipv4.conf.default.log_martians=1"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['ignore_broadcasts']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.icmp_echo_ignore_broadcasts=1"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['ignore_bogus_icmp_errors']:
        script += '''
{
l_output="" l_output2=""
l_parlist="icmp_ignore_bogus_error_responses=1"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['enable_rp_filter']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['enable_syn_cookies']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv4.tcp_syncookies=1"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
KPF
done
}
'''

    if network_config['reject_ipv6_router_adv']:
        script += '''
{
l_output="" l_output2=""
l_parlist="net.ipv6.conf.all.accept_ra=0
net.ipv6.conf.default.accept_ra=0"
l_searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf
/usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf
/etc/sysctl.conf $([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/
{print $2}' /etc/default/ufw)"
KPF()
{
# comment out incorrect parameter(s) in kernel parameter file(s)
l_fafile="$(grep -s -- "^\s*$l_kpname" $l_searchloc | grep -Pv --
"\h*=\h*$l_kpvalue\b\h*" | awk -F: '{print $1}')"
for l_bkpf in $l_fafile; do
echo -e "\n - Commenting out \"$l_kpname\" in \"$l_bkpf\""
sed -ri "/$l_kpname/s/^/# /" "$l_bkpf"
done
# Set correct parameter in a kernel parameter file
if ! grep -Pslq -- "^\h*$l_kpname\h*=\h*$l_kpvalue\b\h*(#.*)?$"
$l_searchloc; then
echo -e "\n - Setting \"$l_kpname\" to \"$l_kpvalue\" in
\"$l_kpfile\""
echo "$l_kpname = $l_kpvalue" >> "$l_kpfile"
fi
# Set correct parameter in active kernel parameters
l_krp="$(sysctl "$l_kpname" | awk -F= '{print $2}' | xargs)"
if [ "$l_krp" != "$l_kpvalue" ]; then
echo -e "\n - Updating \"$l_kpname\" to \"$l_kpvalue\" in the active
kernel parameters"
sysctl -w "$l_kpname=$l_kpvalue"
sysctl -w "$(awk -F'.' '{print $1"."$2".route.flush=1"}' <<<
"$l_kpname")"
fi
}
IPV6F_CHK()
{
l_ipv6s=""
grubfile=$(find /boot -type f \( -name 'grubenv' -o -name 'grub.conf' -
o -name 'grub.cfg' \) -exec grep -Pl -- '^\h*(kernelopts=|linux|kernel)' {}
\;)
if [ -s "$grubfile" ]; then
! grep -P -- "^\h*(kernelopts=|linux|kernel)" "$grubfile" | grep -vq
-- ipv6.disable=1 && l_ipv6s="disabled"
fi
if grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc && \
grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$" $l_searchloc
&& \
sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\h*(#.*)?$" && \
sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
"^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\h*(#.*)?$"; then
l_ipv6s="disabled"
fi
if [ -n "$l_ipv6s" ]; then
echo -e "\n - IPv6 is disabled on the system, \"$l_kpname\" is not
applicable"
else
KPF
fi
}
for l_kpe in $l_parlist; do
l_kpname="$(awk -F= '{print $1}' <<< "$l_kpe")"
l_kpvalue="$(awk -F= '{print $2}' <<< "$l_kpe")"
if grep -q '^net.ipv6.' <<< "$l_kpe"; then
l_kpfile="/etc/sysctl.d/60-netipv6_sysctl.conf"
IPV6F_CHK
else
l_kpfile="/etc/sysctl.d/60-netipv4_sysctl.conf"
KPF
fi
done
}
'''

    disable_protocols = network_config['disable_protocols']
    if disable_protocols['dccp']:
        script += '''
{
l_mname="dccp" # set module name
if ! modprobe -n -v "$l_mname" | grep -P -- '^\h*install
\/bin\/(true|false)'; then
echo -e " - setting module: \"$l_mname\" to be not loadable"
echo -e "install $l_mname /bin/false" >>
/etc/modprobe.d/"$l_mname".conf
fi
if lsmod | grep "$l_mname" > /dev/null 2>&1; then
echo -e " - unloading module \"$l_mname\""
modprobe -r "$l_mname"
fi
if ! grep -Pq -- "^\h*blacklist\h+$l_mname\b" /etc/modprobe.d/*; then
echo -e " - deny listing \"$l_mname\""
echo -e "blacklist $l_mname" >> /etc/modprobe.d/"$l_mname".conf
fi
}
'''

    if disable_protocols['sctp']:
        script += '''
{
l_mname="sctp" # set module name
if ! modprobe -n -v "$l_mname" | grep -P -- '^\h*install
\/bin\/(true|false)'; then
echo -e " - setting module: \"$l_mname\" to be not loadable"
echo -e "install $l_mname /bin/false" >>
/etc/modprobe.d/"$l_mname".conf
fi
if lsmod | grep "$l_mname" > /dev/null 2>&1; then
echo -e " - unloading module \"$l_mname\""
modprobe -r "$l_mname"
fi
if ! grep -Pq -- "^\h*blacklist\h+$l_mname\b" /etc/modprobe.d/*; then
echo -e " - deny listing \"$l_mname\""
echo -e "blacklist $l_mname" >> /etc/modprobe.d/"$l_mname".conf
fi
}
'''

    if disable_protocols['rds']:
        script += '''
{
l_mname="rds" # set module name
if ! modprobe -n -v "$l_mname" | grep -P -- '^\h*install
\/bin\/(true|false)'; then
echo -e " - setting module: \"$l_mname\" to be not loadable"
echo -e "install $l_mname /bin/false" >>
/etc/modprobe.d/"$l_mname".conf
fi
if lsmod | grep "$l_mname" > /dev/null 2>&1; then
echo -e " - unloading module \"$l_mname\""
modprobe -r "$l_mname"
fi
if ! grep -Pq -- "^\h*blacklist\h+$l_mname\b" /etc/modprobe.d/*; then
echo -e " - deny listing \"$l_mname\""
echo -e "blacklist $l_mname" >> /etc/modprobe.d/"$l_mname".conf
fi
}
'''

    if disable_protocols['tipc']:
        script += '''
{
l_mname="tipc" # set module name
if ! modprobe -n -v "$l_mname" | grep -P -- '^\h*install
\/bin\/(true|false)'; then
echo -e " - setting module: \"$l_mname\" to be not loadable"
echo -e "install $l_mname /bin/false" >>
/etc/modprobe.d/"$l_mname".conf
fi
if lsmod | grep "$l_mname" > /dev/null 2>&1; then
echo -e " - unloading module \"$l_mname\""
modprobe -r "$l_mname"
fi
if ! grep -Pq -- "^\h*blacklist\h+$l_mname\b" /etc/modprobe.d/*; then
echo -e " - deny listing \"$l_mname\""
echo -e "blacklist $l_mname" >> /etc/modprobe.d/"$l_mname".conf
fi
}
'''

    return script

if __name__ == '__main__':
    config = config_file.init()
    print(get_script(config))

