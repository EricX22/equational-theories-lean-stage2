% order5_0040  eq1=29201 eq2=25427  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),W),f(Z,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Z,f(X,W))),f(Y,X)) )).
