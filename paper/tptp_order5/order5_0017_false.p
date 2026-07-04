% order5_0017  eq1=10758 eq2=33551  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(f(Z,Z),W))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(f(f(Z,W),Z),X)),U) )).
