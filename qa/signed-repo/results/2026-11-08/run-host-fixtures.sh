date -u
rpm -q yum rpm xcp-hl-release xo-lite-ce xoa-proxy
for v in valid unsigned wrong-key tampered-repomd tampered-primary tampered-rpm outage; do
 echo "CASE=$v"
 yum --disablerepo='*' --enablerepo=qa2-$v clean all
 yum --disablerepo='*' --enablerepo=qa2-$v --setopt=qa2-$v.skip_if_unavailable=0 --setopt=timeout=15 --setopt=retries=1 -y install --downloadonly --downloaddir=/root/qa144-final-$v xo-lite-ce
 echo "EXIT=$?"
done
for v in wrong-key outage; do
 echo "SKIP_CASE=$v"
 yum --disablerepo='*' --enablerepo=qa2-$v clean all
 yum --disablerepo='*' --enablerepo=qa2-$v --setopt=timeout=15 --setopt=retries=1 -y check-update
 echo "EXIT=$?"
done
sha256sum /root/qa144-final-valid/*.rpm
