% order5_0087  eq1=48265 eq2=52936  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(Y,X)),f(W,W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(f(f(X,X),Y),X),Y) )).
