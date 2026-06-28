% hard3_0013  eq1=58 eq2=3050  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,X))) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(f(f(X,X),X),X),X) )).
