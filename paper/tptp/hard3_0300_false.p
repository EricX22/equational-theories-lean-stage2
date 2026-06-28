% hard3_0300  eq1=2848 eq2=1063  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,f(X,X)),X),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(X,f(f(Y,f(Z,Z)),X)) )).
