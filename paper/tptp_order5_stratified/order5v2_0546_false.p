% order5v2_0546  eq1=19917 eq2=20791  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(Z,X)),Z)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,X),f(f(f(Z,Y),W),U)) )).
