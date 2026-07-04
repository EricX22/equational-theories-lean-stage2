% order5_0006  eq1=49823 eq2=15414  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(X,Y) = f(f(Y,f(Y,f(Y,X))),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(f(Y,f(Z,W)),W),W)) )).
