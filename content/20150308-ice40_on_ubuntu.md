Title: Lattice iCEcube2 on Ubuntu 14.04
Date: 2015-03-01 19:00
Category: Projects
Tags: Lattice, iCE40, Linux, Ubuntu


/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/synplify_pro: 186: [: unexpected operator
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/synplify_pro: 200: [: !=: argument expected
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/c_hdl: 186: [: unexpected operator
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/c_hdl: 200: [: !=: argument expected
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/syn_nfilter: 186: [: unexpected operator
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/syn_nfilter: 200: [: !=: argument expected
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/m_generic: 186: [: unexpected operator
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/m_generic: 200: [: !=: argument expected
/home/jan/opt/lscc/iCEcube2.2014.12/synpbase/bin/m_generic: 186: [: unexpected operator


sed -i 's/\/bin\/sh/\/bin\/bash/g' *


jan@jan-ThinkPad-T510 ~/opt/lscc/iCEcube2.2014.12/synpbase/bin
 % for file in $(ls); do sed -i 's/\/bin\/sh/\/bin\/bash/g' $file; done    19:33:27 on 2015-03-07 
sed: couldn't edit config: not a regular file
jan@jan-ThinkPad-T510 ~/opt/lscc/iCEcube2.2014.12/synpbase/bin
 % 


for file in $(ls -la | grep -E '^[^d]' | awk -F "/" '{print $NF}' ); do echo $file; done 




for file in $(ls -la | tail -n +2 | grep -E '^[^d]' | awk '{print $NF}' ); do sed -i 's/\/bin\/sh/\/bin\/bash/g' $file; done 

