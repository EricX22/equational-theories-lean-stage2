% hard3_0338  eq1=3171 eq2=4480  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,Y)) != f(f(Y,X),Y) )).
