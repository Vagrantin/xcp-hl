date -u
rpm -q dnf rpm xoa-hl
for v in valid unsigned wrong-key tampered-repomd tampered-primary tampered-rpm outage; do
 echo "CASE=$v"
 dnf --disablerepo='*' --enablerepo=qa-$v clean all
 dnf --refresh --disablerepo='*' --enablerepo=qa-$v --setopt=qa-$v.skip_if_unavailable=0 --setopt=timeout=15 --setopt=retries=1 -y reinstall --downloadonly --downloaddir=/root/qa144-$v xoa-hl
 echo "EXIT=$?"
done
for v in wrong-key outage; do
 echo "SHIPPED_CASE=$v"
 dnf --disablerepo='*' --enablerepo=qa-$v clean all
 dnf --refresh --disablerepo='*' --enablerepo=qa-$v --setopt=timeout=15 --setopt=retries=1 -y check-update
 echo "EXIT=$?"
done
sha256sum /root/qa144-valid/*.rpm
