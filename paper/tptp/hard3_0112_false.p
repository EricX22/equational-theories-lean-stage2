% hard3_0112  eq1=906 eq2=1231  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(f(Y,X),f(X,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(f(f(X,Y),Y),X)) )).
