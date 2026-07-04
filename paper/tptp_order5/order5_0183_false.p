% order5_0183  eq1=25933 eq2=6392  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),W)),f(Z,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(W,f(f(W,Y),Y)))) )).
