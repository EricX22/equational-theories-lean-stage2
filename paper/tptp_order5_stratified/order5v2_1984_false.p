% order5v2_1984  eq1=7966 eq2=16013  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,f(W,Y)),Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(Z,f(W,Z)),Y),Y)) )).
