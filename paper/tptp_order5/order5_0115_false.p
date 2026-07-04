% order5_0115  eq1=41477 eq2=1111  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),W),W),Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Y,f(X,X)),Z)) )).
