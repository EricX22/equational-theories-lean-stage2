% hard3_0381  eq1=3941 eq2=3936  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,f(Z,Y)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(X,f(Z,X)),Z) )).
