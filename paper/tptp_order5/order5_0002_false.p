% order5_0002  eq1=40162 eq2=61803  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Y,X)),Z),W),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(f(X,X),Y) != f(f(f(Y,Y),Y),Y) )).
