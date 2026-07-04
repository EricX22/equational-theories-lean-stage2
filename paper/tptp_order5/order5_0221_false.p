% order5_0221  eq1=58515 eq2=20669  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),X) = f(Z,f(Z,f(W,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,Y),f(f(f(Z,W),Z),Y)) )).
