% order5v2_1726  eq1=28128 eq2=42333  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,Y)),Z),f(W,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(W,f(Z,f(W,Y)))) )).
