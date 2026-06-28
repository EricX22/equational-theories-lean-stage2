% hard3_0356  eq1=3380 eq2=4171  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Z,f(X,f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Y,Y),Z),Y) )).
