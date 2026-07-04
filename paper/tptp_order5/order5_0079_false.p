% order5_0079  eq1=13425 eq2=10098  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,f(W,U))),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(Y,Z),f(f(X,W),W))) )).
