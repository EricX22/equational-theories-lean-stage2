% order5v2_0761  eq1=37418 eq2=415  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(X,f(Y,Z))),W),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(X,f(X,f(Y,Z)))) )).
