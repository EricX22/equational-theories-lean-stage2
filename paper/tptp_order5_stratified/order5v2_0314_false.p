% order5v2_0314  eq1=35251 eq2=10373  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(W,X),X)),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(Y,Y),f(f(Z,Y),Y))) )).
