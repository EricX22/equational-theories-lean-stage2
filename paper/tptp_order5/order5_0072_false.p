% order5_0072  eq1=6329 eq2=26415  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(f(X,U),Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(f(Z,Z),X)),f(W,Y)) )).
