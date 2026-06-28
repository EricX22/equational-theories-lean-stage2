% hard3_0133  eq1=1054 eq2=2264  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Z)),W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,f(Y,X))),Y) )).
