% order5_0193  eq1=20116 eq2=36803  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(X,f(X,Y)),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),X),f(Y,W)),Z) )).
