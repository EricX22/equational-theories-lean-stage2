% order5v2_0348  eq1=29709 eq2=55420  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Y,f(Z,f(Y,W)))),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(W,f(f(X,X),X)) )).
