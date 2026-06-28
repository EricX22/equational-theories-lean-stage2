% hard3_0033  eq1=172 eq2=4080  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(f(Y,X),X),X) )).
