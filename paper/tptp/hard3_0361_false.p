% hard3_0361  eq1=3490 eq2=3471  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Y,Z),W)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(Y,f(f(X,X),X)) )).
