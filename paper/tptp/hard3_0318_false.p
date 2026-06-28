% hard3_0318  eq1=2931 eq2=2484  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),W),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(f(Y,Z),Z)),X) )).
