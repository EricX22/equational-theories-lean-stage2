% hard3_0100  eq1=796 eq2=1115  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,Y),X))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Y,f(X,Z)),X)) )).
