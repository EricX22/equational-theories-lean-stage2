% order5_0043  eq1=14337 eq2=57807  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(f(W,U),V)),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Y)) = f(f(f(Z,W),Z),W) )).
