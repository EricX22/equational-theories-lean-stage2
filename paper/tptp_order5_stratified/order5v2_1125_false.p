% order5v2_1125  eq1=7212 eq2=13507  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,Y),f(X,Y)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(X,f(f(Y,Z),Y)),W)) )).
