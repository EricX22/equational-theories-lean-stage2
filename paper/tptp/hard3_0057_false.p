% hard3_0057  eq1=372 eq2=315  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(Y,Z),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(Y,f(Y,X)) )).
