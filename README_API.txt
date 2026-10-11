HUONG DAN DEPLOY API PIKAFISH (RENDER)

1) Upload NOi DUNG trong thu muc api/ len GitHub. Khong upload file ZIP nguyen.
2) Neu muon giu api/ la thu muc con trong repo, trong Render Settings:
   Root Directory: api
   Dockerfile Path: ./Dockerfile
   Runtime: Docker; Branch: main; Instance: Free.
3) Neu upload CAC FILE vao goc repo, Root Directory de trong.
4) Commit GitHub, vao Render > Manual Deploy > Deploy latest commit.
5) Kiem tra https://TEN-SERVICE.onrender.com/api/health

CHU Y: Bo cai tai engine va mang NNUE chinh thuc khi Docker build. Chua the xac nhan
thanh cong tren Render thuc te. Ban phat hanh Pikafish hoac Render gioi han RAM/CPU
co the khien buoc build/start that bai. Xem logs de xac dinh.
