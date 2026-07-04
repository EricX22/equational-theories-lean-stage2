% order5v2_0203  eq1=40283 eq2=18772  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,X)),X),X),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,X),f(f(Y,Z),f(Z,Z))) )).
