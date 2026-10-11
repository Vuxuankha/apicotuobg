SUA LOI PIKAFISH RENDER - 2026-10-11

1. Giai nen ZIP. Upload NOI DUNG thu muc api/ len GitHub tai api/; khong upload ZIP nguyen.
2. Render Settings: Root Directory = api ; Dockerfile Path = ./Dockerfile ; Runtime = Docker.
3. Commit GitHub moi, Render > Manual Deploy > Deploy latest commit.
4. Xem log: "BUILD COMMAND". Neu fail, log nay in ra loi bien dich goc (18,000 ky tu cuoi) thay vi chi exit code 2.
5. Sau khi Live: mo https://TEN-DICH-VU.onrender.com/api/health va thu POST /api/analyze.

DA SUA:
- Dung Clang va ARCH=x86-64-universal (theo CI upstream) truoc.
- Thu tiep Clang x86-64 / GCC x86-64 neu cau hinh truoc loi.
- Giu ca cay ma nguon goc khi giai nen (khong chi thu muc src).
- Hien thi loi gcc/clang/Makefile trong logs.

CHUA XAC NHAN: Docker build tren Render va kha nang mang NNUE tuong thich, do moi truong chua download duoc nguon GitHub. Goi Render Free 512MB RAM co the khong du de chay engine trong thoi gian ngan.
