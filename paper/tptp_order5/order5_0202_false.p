% order5_0202  eq1=2940 eq2=11666  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(Y,f(Y,X)),Y),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,f(W,W)),f(W,W))) )).
