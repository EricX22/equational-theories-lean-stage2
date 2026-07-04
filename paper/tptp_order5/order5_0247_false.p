% order5_0247  eq1=33872 eq2=48966  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(X,f(Z,W))),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Y,Y),Z),f(Z,Z)) )).
