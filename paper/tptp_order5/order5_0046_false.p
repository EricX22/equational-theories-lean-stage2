% order5_0046  eq1=2292 eq2=42564  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,f(X,X))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(Y,f(Z,f(f(Y,W),W))) )).
