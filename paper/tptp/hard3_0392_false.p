% hard3_0392  eq1=4404 eq2=4433  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,f(X,Y)) = f(f(X,Z),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(Y,X)) != f(f(X,X),Y) )).
