% order5v2_0027  eq1=2219 eq2=22624  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(Y,Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Y,X)),f(f(Z,W),W)) )).
