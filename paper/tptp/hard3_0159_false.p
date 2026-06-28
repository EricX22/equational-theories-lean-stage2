% hard3_0159  eq1=1340 eq2=4635  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,Y),X) != f(f(Y,X),X) )).
