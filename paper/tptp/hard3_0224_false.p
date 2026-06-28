% hard3_0224  eq1=2083 eq2=1833  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(W,Y)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(X,X)),f(X,Y)) )).
