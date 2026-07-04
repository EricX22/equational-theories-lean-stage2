% order5v2_1233  eq1=38360 eq2=45245  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(X,Z),W)),Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(f(f(X,X),Y),Z)) )).
