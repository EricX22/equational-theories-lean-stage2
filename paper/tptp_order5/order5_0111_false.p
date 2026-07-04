% order5_0111  eq1=13275 eq2=12226  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(Z,f(Y,Z))),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(Z,X),X),f(Z,Z))) )).
