% hard3_0136  eq1=1062 eq2=4271  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Y)),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,X)) != f(X,f(Y,Z)) )).
