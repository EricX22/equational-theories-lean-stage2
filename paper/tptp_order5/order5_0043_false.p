% order5_0043  eq1=14337 eq2=57807  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(f(W,U),V)),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Y)) != f(f(f(Z,W),Z),W) )).
