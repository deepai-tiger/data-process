# science1.pdf pages 1–30 — reviewed LaTeX

- Input: 200 DPI page images; the PDF text layer was not read.
- Scope: all displayed equations and semantic tables found on pages 1–30.
- Recognition: PaddleOCR-VL 1.6 and pix2tex candidates, checked against the rendered page.
- The page-4 table of contents is not treated as a data table.
- Figures and equations printed inside technical drawings are outside this display-equation list.

## Equations

### Page 11

\[
x_w=A_{wc}x_c+b_{wc}
\tag{1-1}
\]

### Page 12

\[
x_w(t)=A_{wc}(t)x_c(t)+b_{wc}(t)
\tag{1-2}
\]

### Page 18

\[
x_p(t)=x_q+b_{pq}(t)
\tag{1-3}
\]

### Page 19

\[
\vec b_{pq}(t)=
\begin{bmatrix}
0 & b_2^{pq}(t) & 0
\end{bmatrix}^{T}
\tag{1-4}
\]

\[
x_p(t)=A_{pq}(t)x_q+b_{pq}
\tag{1-5}
\]

\[
A_{pq}(t)=
\begin{bmatrix}
\cos\phi(t) & -\sin\phi(t) & 0 \\
\sin\phi(t) & \cos\phi(t) & 0 \\
0 & 0 & 1
\end{bmatrix}
\tag{1-6}
\]

\[
\vec b_{pq}=
\begin{bmatrix}
b_1^{pq} & b_2^{pq} & b_3^{pq}
\end{bmatrix}^{T}
\]

\[
\vec b_p(t)=
\begin{bmatrix}
b_1^p & b_2^p & b_3^p
\end{bmatrix}^{T}
\]

\[
x_w(t)=A_{wp0}A_{wp\nu}(t)\bigl(x_p+b_p\bigr)
\tag{1-7}
\]

### Page 21

\[
A_{wp\nu}(t)=
\begin{bmatrix}
\cos\theta_i(t) & 0 & \sin\theta_i(t) \\
0 & 1 & 0 \\
-\sin\theta_i(t) & 0 & \cos\theta_i(t)
\end{bmatrix}
\tag{1-8}
\]

\[
x_q(t)=A_{qc\nu}(t)\bigl(A_{qc0}x_c+r_{c0}\bigr)+b_{qc}(t)
\tag{1-9}
\]

### Page 22

\[
A_{qc\nu}(t)=
\begin{bmatrix}
\cos\psi(t) & 0 & \sin\psi(t) \\
0 & 1 & 0 \\
-\sin\psi(t) & 0 & \cos\psi(t)
\end{bmatrix}
\tag{1-10}
\]

\[
\vec r_{c0}=
\begin{bmatrix}
r_1^{c0} & 0 & r_3^{c0}
\end{bmatrix}^{T}
\tag{1-11}
\]

\[
\begin{aligned}
b_{qc}(t)
  &=\begin{bmatrix}b_1^{qc}(0)&0&b_3^{qc}(0)\end{bmatrix}^{T},\\
b_{qc}(t)
  &=\begin{bmatrix}b_1^{qc}(t)&0&b_3^{qc}(t)\end{bmatrix}^{T}
\end{aligned}
\tag{1-12}
\]

\[
\begin{aligned}
x_w(t)
={}&A_{wp0}A_{wp\nu}(t)
\Bigl\{
A_{qc\nu}(t)\bigl(A_{qc0}x_c+r_{c0}\bigr)\\
&\qquad{}+b_{qc}(t)+b_{pq}(t)+b_p(t)
\Bigr\}
\end{aligned}
\tag{1-13}
\]

\[
\begin{aligned}
b'_{pq}
  &=\begin{bmatrix}0&b_2^{pq}(t)+b_2^p(t)&0\end{bmatrix}^{T},\\
b'(t)
  &=\begin{bmatrix}b_1^p(t)&0&b_3^p(t)\end{bmatrix}^{T}
\end{aligned}
\]

### Page 23

\[
x_w(t)=A_{wp0}A_{wp\nu}(t)
\Bigl\{
A_{pq}(t)A_{qc\nu}(t)
\bigl(A_{qc0}x_c+r_{c0}\bigr)
b_{qc}+b'_p(t)
\Bigr\}
\]

\[
x_w(t)=A_{wp0}A_{wp\nu}(t)
\Bigl\{
A_{pq}(t)A_{qc\nu}(t)
\bigl(A_{qc0}x_c+r_{c0}\bigr)
b_{qc}(t)+\bar b_p(t)
\Bigr\}
\tag{1-14}
\]

\[
\begin{aligned}
A'_{wp0}&=A_{wp0}A_{qc0},\\
A'_{wp\nu}(t)
  &=A_{qc0}^{-1}A_{wp\nu}(t)A_{qc\nu}(t)A_{qc0}
\end{aligned}
\tag{1-15}
\]

### Page 24

\[
b'_p(t)
=A_{qc\nu}^{-1}r_{c0}
+A_{pc0}^{-1}A_{qc\nu}^{-1}(t)
\bigl[b_{qc}(t)+b_p(t)\bigr]
\tag{1-16}
\]

\[
x_w(t)
=A'_{wp0}A'_{wp\nu}(t)
\bigl[x_c+b_{pq}(t)+b'_p(t)\bigr]
\tag{1-17}
\]

\[
A'_{wp0}A'_{wp\nu}(t)b_{pq}(t)
=A_{wp0}A_{wp\nu}(t)b_{pq}(t)
\tag{1-18}
\]

\[
\begin{aligned}
b'_{qc}(t)
  &=\begin{bmatrix}b_1^{qc}(t)&0&0\end{bmatrix}^{T},\\
b'_p(t)
  &=\begin{bmatrix}
      b_1^p(t)&b_2^p(t)&b_3^p(t)+b_p^{qc}(t)
    \end{bmatrix}^{T}
\end{aligned}
\tag{1-19}
\]

### Page 25

\[
x_w(t)=A_{wp0}A_{wp\nu}(t)
\Bigl\{
A_{pq}(t)A_{qc\nu}(t)
\bigl(A_{pq0}x_c+r_{c0}\bigr)
b'_{qc}(t)+b'_p(t)
\Bigr\}
\tag{1-20}
\]

## Tables

### Page 23 — Table 1-1

\[
\begin{array}{|c|c|l|}
\hline
\text{창성운동} & \text{창성운동축} & \text{좌표축의 관계} \\
\hline
\text{직선창성운동}
& Y_p\text{축방향}
& \begin{gathered}
  Y_p\text{축}=Y_q\text{축},\quad
  Y_p\text{축}\parallel Y_q\text{축},\quad
  Z_p\text{축}\parallel Z_q\text{축},\\
  X_p\text{축}\parallel X_q\text{축}
  \end{gathered} \\
\hline
\text{회전창성운동}
& Z_q\text{축주위}
& Z_p\text{축}=Z_q\text{축},\quad
  Y_p\text{축}\parallel Y_q\text{축} \\
\hline
\end{array}
\tag{표 1-1}
\]

### Page 29 — Table 1-2

\[
\begin{array}{|l|c|c|c|c|c|c|c|}
\hline
\begin{gathered}\text{I형 보내기}\\\text{보내기운동}\end{gathered}
& I_1 & I_2 & I_3 & I_4 & I_5 & I_6 & I_7 \\
\hline
\text{공구쪽 보내기 }b_1^{qc}(t)
& 0 & & & 0 & & 0 & 0 \\
\hline
\text{가공품쪽 보내기 }b_3^p(t)
& & 0 & & 0 & 0 & & 0 \\
\hline
\text{공구쪽 회전보내기 }\psi(t)
& & & 0 & & 0 & 0 & 0 \\
\hline
\end{array}
\tag{표 1-2}
\]

### Page 30 — Table 1-3

\[
\begin{array}{|c|c|c|c|}
\hline
\begin{gathered}\text{단위창성되는 면}\\\text{II형 보내기}\end{gathered}
& \text{직선}
& \text{평면}
& \text{곡면(자름면형태 일정)} \\
\hline
\mathrm{II}\Phi
& -
& \text{평면}
& \text{곡면(자름면형태 일정)} \\
\hline
\mathrm{II}1
& \text{평면}
& \text{평면}
& \text{평면} \\
\hline
\mathrm{II}2
& \text{원통면(외면)}
& \text{원통면(외면)}
& \text{원통면(외면)} \\
\hline
\mathrm{II}3
& \text{곡면(자름면 형태일정)}
& \text{곡면(자름면 형태일정)}
& \text{곡면(자름면형태 일정)} \\
\hline
\end{array}
\tag{표 1-3}
\]
