% hard3_0247  eq1=2255 eq2=2487  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(Y,f(X,X))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(X,f(f(Y,Z),Z)),W) )).
