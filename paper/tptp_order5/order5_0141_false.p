% order5_0141  eq1=48536 eq2=3978  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,U)),f(U,U)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Y,f(Z,Y)),W) )).
