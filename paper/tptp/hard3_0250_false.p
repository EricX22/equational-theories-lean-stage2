% hard3_0250  eq1=2265 eq2=3337  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,X))),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(Z,f(W,X))) )).
