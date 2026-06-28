% hard3_0389  eq1=4217 eq2=4362  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Y),Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(Y,f(X,Z)) )).
